import { Injectable, inject } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { API_URL } from '../config/api';
import { Orden, OrdenPayload, ResumenOrdenes } from '../models/orden';

@Injectable({ providedIn: 'root' })
export class OrdenService {
  private http = inject(HttpClient);
  private apiUrl = `${API_URL}/ordenes`;

  // Barra final intencional en la colección: evita el redirect 307 de FastAPI
  getOrdenes(): Observable<Orden[]> { return this.http.get<Orden[]>(`${this.apiUrl}/`); }
  getResumen(): Observable<ResumenOrdenes> { return this.http.get<ResumenOrdenes>(`${this.apiUrl}/resumen`); }
  getOrden(id: number): Observable<Orden> { return this.http.get<Orden>(`${this.apiUrl}/${id}`); }
  createOrden(orden: OrdenPayload): Observable<Orden> { return this.http.post<Orden>(`${this.apiUrl}/`, orden); }
  updateOrden(id: number, orden: Partial<OrdenPayload>): Observable<Orden> { return this.http.put<Orden>(`${this.apiUrl}/${id}`, orden); }
  deleteOrden(id: number): Observable<void> { return this.http.delete<void>(`${this.apiUrl}/${id}`); }
}
