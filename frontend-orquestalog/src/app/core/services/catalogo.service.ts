import { Injectable, inject } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { API_URL } from '../config/api';
import { Centro, Flota, Ruta } from '../models/catalogos';

@Injectable({ providedIn: 'root' })
export class CatalogoService {
  private http = inject(HttpClient);

  getCentros(): Observable<Centro[]> { return this.http.get<Centro[]>(`${API_URL}/centros`); }
  getFlotas(): Observable<Flota[]> { return this.http.get<Flota[]>(`${API_URL}/flotas`); }
  getRutas(): Observable<Ruta[]> { return this.http.get<Ruta[]>(`${API_URL}/rutas`); }
}
