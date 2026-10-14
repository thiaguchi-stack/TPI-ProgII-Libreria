from __future__ import annotations

from datetime import datetime, timezone
from decimal import Decimal
from typing import List, Optional

from sqlalchemy import CheckConstraint, Column, Numeric, PrimaryKeyConstraint
from sqlalchemy.orm import Mapped, relationship
from sqlmodel import Field, Relationship, SQLModel


class Editorial(SQLModel, table=True):
    __tablename__ = "editorial"

    id: Optional[int] = Field(default=None, primary_key=True)
    nombre: str = Field(unique=True)
    pais: Optional[str] = None

    libros: List["Libro"] = Relationship(sa_relationship=relationship("Libro", back_populates="editorial"))


class Genero(SQLModel, table=True):
    __tablename__ = "genero"

    id: Optional[int] = Field(default=None, primary_key=True)
    nombre: str = Field(unique=True)

    libros: List["Libro"] = Relationship(sa_relationship=relationship("Libro", back_populates="genero"))


class Autor(SQLModel, table=True):
    __tablename__ = "autor"

    id: Optional[int] = Field(default=None, primary_key=True)
    nombre: str
    nacionalidad: Optional[str] = None

    autorias: List["LibroAutor"] = Relationship(sa_relationship=relationship("LibroAutor", back_populates="autor"))


class Libro(SQLModel, table=True):
    __tablename__ = "libro"
    __table_args__ = (
        CheckConstraint("precio > 0", name="ck_libro_precio_positivo"),
        CheckConstraint("stock >= 0", name="ck_libro_stock_no_negativo"),
    )

    id: Optional[int] = Field(default=None, primary_key=True)
    isbn: str = Field(unique=True)
    titulo: str
    precio: Decimal = Field(sa_column=Column(Numeric(10, 2), nullable=False))
    stock: int = Field(default=0)
    editorial_id: int = Field(foreign_key="editorial.id", index=True)
    genero_id: Optional[int] = Field(default=None, foreign_key="genero.id", index=True)

    editorial: Editorial = Relationship(sa_relationship=relationship("Editorial", back_populates="libros"))
    genero: Optional[Genero] = Relationship(sa_relationship=relationship("Genero", back_populates="libros"))
    autorias: List["LibroAutor"] = Relationship(sa_relationship=relationship("LibroAutor", back_populates="libro"))
    renglones: List["RenglonVenta"] = Relationship(sa_relationship=relationship("RenglonVenta", back_populates="libro"))


class LibroAutor(SQLModel, table=True):
    __tablename__ = "libro_autor"
    __table_args__ = (
        PrimaryKeyConstraint("libro_id", "autor_id", name="pk_libro_autor"),
        CheckConstraint("orden >= 1", name="ck_libro_autor_orden_positivo"),
        CheckConstraint(
            "rol IN ('autor', 'coautor', 'traductor', 'ilustrador')",
            name="ck_libro_autor_rol_valido",
        ),
    )

    libro_id: int = Field(foreign_key="libro.id", primary_key=True, index=True)
    autor_id: int = Field(foreign_key="autor.id", primary_key=True, index=True)
    rol: str
    orden: int

    libro: Libro = Relationship(sa_relationship=relationship("Libro", back_populates="autorias"))
    autor: Autor = Relationship(sa_relationship=relationship("Autor", back_populates="autorias"))


class Cliente(SQLModel, table=True):
    __tablename__ = "cliente"

    id: Optional[int] = Field(default=None, primary_key=True)
    nombre: str
    email: str = Field(unique=True)

    perfil: Optional["PerfilCliente"] = Relationship(sa_relationship=relationship("PerfilCliente", back_populates="cliente"))
    ventas: List["Venta"] = Relationship(sa_relationship=relationship("Venta", back_populates="cliente"))


class PerfilCliente(SQLModel, table=True):
    __tablename__ = "perfil_cliente"

    id: Optional[int] = Field(default=None, primary_key=True)
    cliente_id: int = Field(foreign_key="cliente.id", unique=True, index=True)
    telefono: Optional[str] = None
    direccion: Optional[str] = None

    cliente: Cliente = Relationship(sa_relationship=relationship("Cliente", back_populates="perfil"))


class Venta(SQLModel, table=True):
    __tablename__ = "venta"
    __table_args__ = (
        CheckConstraint("total >= 0", name="ck_venta_total_no_negativo"),
    )

    id: Optional[int] = Field(default=None, primary_key=True)
    cliente_id: int = Field(foreign_key="cliente.id", index=True)
    fecha: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    total: Decimal = Field(sa_column=Column(Numeric(12, 2), nullable=False))

    cliente: Cliente = Relationship(sa_relationship=relationship("Cliente", back_populates="ventas"))
    renglones: List["RenglonVenta"] = Relationship(sa_relationship=relationship("RenglonVenta", back_populates="venta"))


class RenglonVenta(SQLModel, table=True):
    __tablename__ = "renglon_venta"
    __table_args__ = (
        CheckConstraint("cantidad > 0", name="ck_renglon_cantidad_positiva"),
        CheckConstraint("precio_unitario > 0", name="ck_renglon_precio_positivo"),
    )

    id: Optional[int] = Field(default=None, primary_key=True)
    venta_id: int = Field(foreign_key="venta.id", index=True)
    libro_id: int = Field(foreign_key="libro.id", index=True)
    cantidad: int
    precio_unitario: Decimal = Field(sa_column=Column(Numeric(10, 2), nullable=False))

    venta: Venta = Relationship(sa_relationship=relationship("Venta", back_populates="renglones"))
    libro: Libro = Relationship(sa_relationship=relationship("Libro", back_populates="renglones"))




