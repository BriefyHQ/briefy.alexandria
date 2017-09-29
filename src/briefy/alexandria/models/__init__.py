"""briefy.alexandria models."""
from briefy.alexandria.models.asset import Asset  # noQA
from briefy.alexandria.models.base import AssetsCollection  # noQA
from briefy.alexandria.models.collection import Collection  # noQA


ALL_MODELS = [
    Asset,
    AssetsCollection,
    Collection
]
