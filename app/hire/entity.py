import dataclasses
from typing import List, Optional


@dataclasses.dataclass
class ProductEntity:
    name: str
    price: int

@dataclasses.dataclass
class OrderEntity:
    start: str
    end: str
    total_price: Optional[int] = None

@dataclasses.dataclass
class OrderedProductEntity:
    product: ProductEntity
    order: OrderEntity
    duration: int
    order_price: int