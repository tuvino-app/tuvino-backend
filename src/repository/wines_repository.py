import uuid
from fastapi import HTTPException
import logging

from src.repository.base import BaseRepository, Session

class WinesRepository(BaseRepository):
    def __init__(self, session: Session):
        super().__init__(session)

    _table_name = "wines"

    def get_preference_options(self):
        return {
            'types': {
                0: 'Tinto – Rico y profundo en sabor',
                1: 'Blanco – Ligero y refrescante',
                2: 'Rosado – Una combinación de características de vinos tintos y blancos',
                3: 'Espumoso – Burbujeante y festivo',
                4: 'No sabe/no contesta'
            },
            'bodies': {
                0: 'Muy ligero – como un sorbo delicado sin mucha presencia',
                2: 'Ligero – con algo más de presencia que el agua',
                3: 'Medio – equilibrado y fácil de beber',
                4: 'Robusto – un vino con sustancia notable',
                5: 'De cuerpo completo – intenso, robusto y con mucha presencia en el paladar',
                6: 'No sabe/no contesta'
            },
            'intensities': {
                0: 'Muy sutil – una insinuación apenas perceptible del sabor',
                1: 'Suave – presente sin llegar a ser abrumador',
                2: 'Equilibrada – una buena mezcla de sabores que se hacen notar de manera constante',
                3: 'Intensa – los sabores se destacan con claridad',
                4: 'Muy intensa – una explosión de sabor en cada sorbo',
                5: 'No sabe/no contesta'
            },
            'dryness': {
                0: 'Muy suave – sin sensación alguna de sequedad',
                1: 'Mayormente suave – con un leve toque de sequedad',
                2: 'Con una textura moderada – equilibrado, entre suavidad y un toque de sequedad',
                3: 'Con textura marcada – se nota algo de sequedad en la lengua',
                4: 'Con fuerte textura – una sensación de sequedad pronunciada que le da estructura al vino',
                5: 'No sabe/no contesta'
            },
            'abv': {
                0: 'Suave',
                1: 'Moderado',
                2: 'Alto contenido alcohólico',
                3: 'No sabe/no contesta'
            }
        }