export interface Orden {
  id?: number;
  descripcion: string;
  fecha_creacion?: string;
  estado: string;
  centro_distribucion_id: number;
  flota_id: number;
  ruta_id: number;
  empresa_id?: number;
}

export type OrdenPayload = Pick<
  Orden,
  'descripcion' | 'estado' | 'centro_distribucion_id' | 'flota_id' | 'ruta_id'
>;

export interface ResumenOrdenes {
  total: number;
  pendientes: number;
  en_proceso: number;
  completadas: number;
}
