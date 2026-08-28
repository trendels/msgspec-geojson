# msgspec-geojson

A collection of [GeoJSON] types for [msgspec].

Inspired by the [msgspec GeoJSON example code][geojson_example] and [geojson-pydantic].

[GeoJSON]: https://geojson.org
[msgspec]: https://msgspec.dev/
[geojson_example]: https://msgspec.dev/examples/geojson
[geojson-pydantic]: https://pypi.org/project/geojson-pydantic/

This lets you parse GeoJSON into type-safe objects, including properties, and
serialize those objects back to GeoJSON:

~~~python
>>> import msgspec.json
>>> from msgspec import Struct
>>> from msgspec_geojson import Feature, Point

>>> class PoiProperties(Struct):
...    name: str
...    kind: str

>>> obj = msgspec.json.decode("""
...     {"type": "Feature", "id": 1,
...      "properties": {"name": "Zoo Zürich", "kind": "tourism/zoo"},
...      "geometry": {"type": "Point", "coordinates": [8.574695, 47.384510]}}
... """, type=Feature[Point, PoiProperties])

>>> obj.id
1
>>> obj.geometry
Point(coordinates=(8.574695, 47.38451))
>>> obj.properties
PoiProperties(name='Zoo Zürich', kind='tourism/zoo')

>>> feature = Feature(
...     Point(coordinates=(7.5823576, 47.5489249)),
...     PoiProperties(name="Zoo Basel", kind="tourism/zoo"),
... )
>>> msgspec.json.encode(feature)
b'{"type":"Feature","geometry":{"type":"Point","coordinates":[7.5823576,47.5489249]},"properties":{"name":"Zoo Basel","kind":"tourism/zoo"}}'

~~~

