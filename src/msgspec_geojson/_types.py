from typing import Any

from msgspec import UNSET, Struct, UnsetType

type Position = tuple[float, float]


class Point(Struct, tag=True):
    """A GeoJSON Point Geometry"""

    coordinates: Position


class MultiPoint(Struct, tag=True):
    """A GeoJSON MultiPoint Geometry"""

    coordinates: list[Position]


class LineString(Struct, tag=True):
    """A GeoJSON LineString Geometry"""

    coordinates: list[Position]


class MultiLineString(Struct, tag=True):
    """A GeoJSON MultiLineString Geometry"""

    coordinates: list[list[Position]]


class Polygon(Struct, tag=True):
    """A GeoJSON Polygon Geometry"""

    coordinates: list[list[Position]]


class MultiPolygon(Struct, tag=True):
    """A GeoJSON MultiPolygon Geometry"""

    coordinates: list[list[list[Position]]]


class GeometryCollection(Struct, tag=True):
    """A GeoJSON GeometryCollection"""

    geometries: list["Geometry"]


type Geometry = (
    Point
    | MultiPoint
    | LineString
    | MultiLineString
    | Polygon
    | MultiPolygon
    | GeometryCollection
)


class Feature[G: Geometry | None, P](Struct, tag=True):
    """A GeoJSON Feature"""

    geometry: G
    properties: P
    id: str | int | UnsetType = UNSET
    bbox: tuple[float, float, float, float] | UnsetType = UNSET


class FeatureCollection[F: Feature[Any, Any]](Struct, tag=True):
    """A GeoJSON FeatureCollection"""

    features: list[F]
    bbox: tuple[float, float, float, float] | UnsetType = UNSET


type GeoJSON = (
    Geometry | Feature[Geometry, Any] | FeatureCollection[Feature[Geometry, Any]]
)
