import { Component, inject } from '@angular/core';
import { RouterModule } from '@angular/router';
import { CommonModule } from '@angular/common';
import { AuthService } from './core/services/auth.service';
import { ToastComponent } from './core/components/toast/toast.component';

@Component({
  selector: 'app-root',
  standalone: true,
  imports: [RouterModule, CommonModule, ToastComponent],
  templateUrl: './app.component.html'
})
export class AppComponent {
  auth = inject(AuthService);

  private readonly roles: Record<string, string> = {
    admin: 'Administrador',
    gestor: 'Gestor logístico',
    conductor: 'Conductor'
  };

  etiquetaRol(): string {
    const rol = this.auth.getPayload()?.rol ?? '';
    return this.roles[rol] ?? rol;
  }

  cerrarSesion() {
    this.auth.logout();
  }
}
