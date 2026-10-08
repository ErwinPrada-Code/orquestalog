import { Injectable, inject } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Observable } from 'rxjs';
import { Orden } from '../models/orden';

@Injectable({
  providedIn: 'root'
})
export class OrdenService {
  private http = inject(HttpClient);
  private apiUrl = 'http://127.0.0.1:8000/api/v1/ordenes';

  // Lee el token guardado tras el inicio de sesión
  private getOptions() {
    const token = localStorage.getItem('token');
    return { headers: new HttpHeaders({ 'Authorization': `Bearer ${token}` }) };
  }

  getOrdenes(): Observable<Orden[]> { return this.http.get<Orden[]>(`${this.apiUrl}/`, this.getOptions()); }
  getOrden(id: number): Observable<Orden> { return this.http.get<Orden>(`${this.apiUrl}/${id}`, this.getOptions()); }
  createOrden(orden: Orden): Observable<Orden> { return this.http.post<Orden>(`${this.apiUrl}/`, orden, this.getOptions()); }
  updateOrden(id: number, orden: Partial<Orden>): Observable<Orden> { return this.http.put<Orden>(`${this.apiUrl}/${id}`, orden, this.getOptions()); }
  deleteOrden(id: number): Observable<void> { return this.http.delete<void>(`${this.apiUrl}/${id}`, this.getOptions()); }
}
