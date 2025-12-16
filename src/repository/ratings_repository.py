import logging
from typing import List, Optional

from src.utilities.supabase_client import supabase
from src.models.rating import Rating
from src.models.wine import Wine


class WineRatingsRepository:
    """Repository for wine ratings operations using Supabase"""

    def get_by_user_id_and_wine_id(self, user_id: str, wine_id: int) -> Optional[Rating]:
        """Get a specific rating by user and wine"""
        try:
            response = supabase.table("wine_ratings")\
                .select("*")\
                .eq("user_id", user_id)\
                .eq("wine_id", wine_id)\
                .execute()

            # Check if any results were returned
            if not response.data or len(response.data) == 0:
                return None

            rating_data = response.data[0]

            # Fetch wine data separately
            wine_response = supabase.table("wines")\
                .select("*")\
                .eq("wine_id", wine_id)\
                .execute()

            if not wine_response.data or len(wine_response.data) == 0:
                return None

            wine_data = wine_response.data[0]
            wine = Wine(
                wine_data['wine_id'],
                wine_data['wine_name'],
                wine_data['type'],
                wine_data['elaborate'],
                wine_data['abv'],
                wine_data['body'],
                wine_data['country'],
                wine_data['region'],
                wine_data['winery'],
                wine_data.get('summary')
            )

            return Rating(
                rating_data['user_id'],
                wine,
                rating_data.get('rating'),
                rating_data.get('review')
            )
        except Exception as e:
            logging.error(f"Error in get_by_user_id_and_wine_id: {e}")
            return None

    def get_by_user_id(self, user_id: str) -> List[Rating]:
        """Get all ratings by a user"""
        response = supabase.table("wine_ratings")\
            .select("*")\
            .eq("user_id", user_id)\
            .order("date", desc=True)\
            .execute()

        ratings = []
        if response.data:
            # Get unique wine IDs from ratings
            wine_ids = list(set(r['wine_id'] for r in response.data))

            # Fetch wine details
            wines_map = {}
            if wine_ids:
                wines_response = supabase.table("wines")\
                    .select("*")\
                    .in_("wine_id", wine_ids)\
                    .execute()

                if wines_response.data:
                    wines_map = {w['wine_id']: w for w in wines_response.data}

            # Build ratings with wine data
            for rating_data in response.data:
                wine_data = wines_map.get(rating_data['wine_id'])
                if wine_data:
                    wine = Wine(
                        wine_data['wine_id'],
                        wine_data['wine_name'],
                        wine_data['type'],
                        wine_data['elaborate'],
                        wine_data['abv'],
                        wine_data['body'],
                        wine_data['country'],
                        wine_data['region'],
                        wine_data['winery'],
                        wine_data.get('summary')
                    )
                    ratings.append(Rating(
                        rating_data['user_id'],
                        wine,
                        rating_data.get('rating'),
                        rating_data.get('review')
                    ))
        return ratings

    def get_by_wine_id(self, wine_id: int) -> List[Rating]:
        """Get all ratings for a specific wine"""
        response = supabase.table("wine_ratings")\
            .select("*")\
            .eq("wine_id", wine_id)\
            .order("date", desc=True)\
            .execute()

        ratings = []
        if response.data:
            # Fetch wine data once (since all ratings are for the same wine)
            wine_response = supabase.table("wines")\
                .select("*")\
                .eq("wine_id", wine_id)\
                .execute()

            wine_data = None
            if wine_response.data and len(wine_response.data) > 0:
                wine_data = wine_response.data[0]

            if wine_data:
                wine = Wine(
                    wine_data['wine_id'],
                    wine_data['wine_name'],
                    wine_data['type'],
                    wine_data['elaborate'],
                    wine_data['abv'],
                    wine_data['body'],
                    wine_data['country'],
                    wine_data['region'],
                    wine_data['winery'],
                    wine_data.get('summary')
                )

                for rating_data in response.data:
                    ratings.append(Rating(
                        rating_data['user_id'],
                        wine,
                        rating_data.get('rating'),
                        rating_data.get('review')
                    ))
        return ratings

    def save(self, rating: Rating) -> bool:
        """Save or update a wine rating"""
        try:
            from datetime import datetime, timezone

            current_datetime = datetime.now(timezone.utc)
            
            # Check if rating already exists
            existing = self.get_by_user_id_and_wine_id(str(rating.user_id), rating.wine.wine_id)

            review_value = None
            if rating.review is not None:
                if isinstance(rating.review, str) and rating.review.strip():
                    review_value = rating.review.strip()
            
            rating_data = {
                "user_id": str(rating.user_id),
                "wine_id": rating.wine.wine_id,
                "rating": rating.rating,
                "review": review_value,
                "date": current_datetime.isoformat(),
                "year": current_datetime.year
            }

            if existing:
                # Update existing rating
                supabase.table("wine_ratings")\
                    .update(rating_data)\
                    .eq("user_id", str(rating.user_id))\
                    .eq("wine_id", rating.wine.wine_id)\
                    .execute()
            else:
                # Insert new rating
                supabase.table("wine_ratings").insert(rating_data).execute()

            return True
        except Exception as e:
            logging.error(f'Error saving rating: {e}')
            return False
