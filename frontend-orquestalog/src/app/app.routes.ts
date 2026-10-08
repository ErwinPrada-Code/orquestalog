import { Routes } from '@angular/router';
import { ListadoOrdenesComponent } from './features/ordenes/listado-ordenes/listado-ordenes.component';
import { FormularioOrdenComponent } from './features/ordenes/formulario-orden/formulario-orden.component';
import { LoginComponent } from './features/auth/login/login.component';
import { DetalleOrdenComponent } from './features/ordenes/detalle-orden/detalle-orden.component';
import { DashboardComponent } from './features/dashboard/dashboard.component'; // <-- Importación
import { authGuard } from './core/guards/auth.guard';

export const routes: Routes = [
  { path: '', redirectTo: 'login', pathMatch: 'full' }, // <-- Ahora redirige al login primero
  { path: 'login', component: LoginComponent },
  { path: 'dashboard', component: DashboardComponent, canActivate: [authGuard] }, // <-- Ruta del Dashboard
  { path: 'ordenes', component: ListadoOrdenesComponent, canActivate: [authGuard] },
  { path: 'ordenes/nueva', component: FormularioOrdenComponent, canActivate: [authGuard] },
  { path: 'ordenes/editar/:id', component: FormularioOrdenComponent, canActivate: [authGuard] },
  { path: 'ordenes/detalle/:id', component: DetalleOrdenComponent, canActivate: [authGuard] } // <-- Nueva ruta de detalle
];
