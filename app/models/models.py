from sqlalchemy import Column, Integer, String, BigInteger, ForeignKey, DECIMAL, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.core.database import Base

class Empresa(Base):
    __tablename__ = "empresas"
    id = Column(BigInteger, primary_key=True, index=True)
    nombre = Column(String, nullable=False)
    direccion = Column(String)
    telefono = Column(String)
    email = Column(String)

    usuarios = relationship("Usuario", back_populates="empresa")
    centros = relationship("CentroDistribucion", back_populates="empresa")
    flotas = relationship("Flota", back_populates="empresa")
    rutas = relationship("Ruta", back_populates="empresa")
    ordenes = relationship("Orden", back_populates="empresa")

class Usuario(Base):
    __tablename__ = "usuarios"
    id = Column(BigInteger, primary_key=True, index=True)
    nombre = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    rol = Column(String, nullable=False) # admin, gestor, conductor
    empresa_id = Column(BigInteger, ForeignKey("empresas.id"), nullable=False)

    empresa = relationship("Empresa", back_populates="usuarios")

class CentroDistribucion(Base):
    __tablename__ = "centros_distribucion"
    id = Column(BigInteger, primary_key=True, index=True)
    nombre = Column(String, nullable=False)
    direccion = Column(String, nullable=False)
    empresa_id = Column(BigInteger, ForeignKey("empresas.id"), nullable=False)

    empresa = relationship("Empresa", back_populates="centros")
    ordenes = relationship("Orden", back_populates="centro")

class Flota(Base):
    __tablename__ = "flotas"
    id = Column(BigInteger, primary_key=True, index=True)
    nombre = Column(String, nullable=False)
    tipo = Column(String, nullable=False)
    capacidad = Column(Integer, nullable=False)
    empresa_id = Column(BigInteger, ForeignKey("empresas.id"), nullable=False)

    empresa = relationship("Empresa", back_populates="flotas")
    ordenes = relationship("Orden", back_populates="flota")

class Ruta(Base):
    __tablename__ = "rutas"
    id = Column(BigInteger, primary_key=True, index=True)
    origen = Column(String, nullable=False)
    destino = Column(String, nullable=False)
    distancia_km = Column(DECIMAL, nullable=False)
    tiempo_estimado_minutos = Column(Integer, nullable=False)
    empresa_id = Column(BigInteger, ForeignKey("empresas.id"), nullable=False)

    empresa = relationship("Empresa", back_populates="rutas")
    ordenes = relationship("Orden", back_populates="ruta")

class Orden(Base):
    __tablename__ = "ordenes"
    id = Column(BigInteger, primary_key=True, index=True)
    descripcion = Column(String, nullable=False)
    fecha_creacion = Column(DateTime(timezone=True), server_default=func.now())
    estado = Column(String, nullable=False)
    centro_distribucion_id = Column(BigInteger, ForeignKey("centros_distribucion.id"), nullable=False)
    flota_id = Column(BigInteger, ForeignKey("flotas.id"), nullable=False)
    ruta_id = Column(BigInteger, ForeignKey("rutas.id"), nullable=False)
    empresa_id = Column(BigInteger, ForeignKey("empresas.id"), nullable=False)

    centro = relationship("CentroDistribucion", back_populates="ordenes")
    flota = relationship("Flota", back_populates="ordenes")
    ruta = relationship("Ruta", back_populates="ordenes")
    empresa = relationship("Empresa", back_populates="ordenes")