import { Routes } from '@angular/router';
import { ListadoOrdenesComponent } from './features/ordenes/listado-ordenes/listado-ordenes.component';
import { FormularioOrdenComponent } from './features/ordenes/formulario-orden/formulario-orden.component';
import { LoginComponent } from './features/auth/login/login.component';
import { DetalleOrdenComponent } from './features/ordenes/detalle-orden/detalle-orden.component';
import { DashboardComponent } from './features/dashboard/dashboard.component';
import { ListadoFlotasComponent } from './features/flotas/listado-flotas/listado-flotas.component';
import { FormularioFlotaComponent } from './features/flotas/formulario-flota/formulario-flota.component';
import { authGuard } from './core/guards/auth.guard';
import { roleGuard } from './core/guards/role.guard';

export const routes: Routes = [
  { path: '', redirectTo: 'login', pathMatch: 'full' },
  { path: 'login', component: LoginComponent },
  { path: 'dashboard', component: DashboardComponent, canActivate: [authGuard] },
  { path: 'ordenes', component: ListadoOrdenesComponent, canActivate: [authGuard] },
  {
    path: 'ordenes/nueva',
    component: FormularioOrdenComponent,
    canActivate: [authGuard, roleGuard('admin', 'gestor')],
  },
  {
    path: 'ordenes/editar/:id',
    component: FormularioOrdenComponent,
    canActivate: [authGuard, roleGuard('admin', 'gestor')],
  },
  { path: 'ordenes/detalle/:id', component: DetalleOrdenComponent, canActivate: [authGuard] },
  { path: 'flotas', component: ListadoFlotasComponent, canActivate: [authGuard, roleGuard('admin')] },
  { path: 'flotas/nueva', component: FormularioFlotaComponent, canActivate: [authGuard, roleGuard('admin')] },
  { path: 'flotas/editar/:id', component: FormularioFlotaComponent, canActivate: [authGuard, roleGuard('admin')] },
];
