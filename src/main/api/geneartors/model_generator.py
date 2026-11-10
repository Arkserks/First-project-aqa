import random
import uuid
from typing import Any, get_type_hints, get_origin, Annotated, get_args

from src.main.api.geneartors.creation_rule import CreationRule

import rstr


class RandomModelGenerator:
    @staticmethod
    def generate(cls: type) -> Any:
        type_hints = get_type_hints(cls, include_extras=True)
        init_data = {}

        for field_name, annotated_type in type_hints.items():
            rule = None
            actual_type = annotated_type

            if get_origin(annotated_type) is Annotated:
                actual_type, *annotations = get_args(annotated_type)
                for ann in annotations:
                    if isinstance(ann, CreationRule):
                        rule = ann

            if rule:
                value = RandomModelGenerator._generate_from_regex(rule.regex, actual_type)
            else:
                raise ValueError(
                    f"У поля '{field_name}' нет CreationRule — это runtime-значение, "
                    f"его нельзя сгенерировать"
                )

            init_data[field_name] = value

        return cls(**init_data)


    @staticmethod
    def _generate_from_regex(regex: str, field_type: type) -> Any:
        generated = rstr.xeger(regex)
        if field_type is int:
            return int(generated)
        if field_type is float:
            return float(generated)
        return generated


    @staticmethod
    def _generate_value(field_type: type) -> Any:
        if field_type is str:
            return str(uuid.uuid4())[:8]
        elif field_type is int:
            return random.randint(1, 9999)
        elif field_type is float:
            return round(random.uniform(0, 100), 2)
        elif field_type is bool:
            return random.choice([True, False])
        elif field_type is list:
            return [str(uuid.uuid4())[:5]]
        elif isinstance(field_type, type):
            return RandomModelGenerator.generate(field_type)
        return None

    @staticmethod
    def generate_field(cls: type, field_name: str) -> Any:
        """Значение одного поля по его CreationRule."""
        hints = get_type_hints(cls, include_extras=True)
        annotated_type = hints[field_name]

        if get_origin(annotated_type) is Annotated:
            actual_type, *annotations = get_args(annotated_type)
        else:
            actual_type, annotations = annotated_type, []

        rule = next((a for a in annotations if isinstance(a, CreationRule)), None)
        if rule is None:
            raise ValueError(f"У поля '{field_name}' нет CreationRule")

        return RandomModelGenerator._generate_from_regex(rule.regex, actual_type)