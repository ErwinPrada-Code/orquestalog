import { Component, inject } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { Router } from '@angular/router';
import { AuthService } from '../../../core/services/auth.service';

@Component({
  selector: 'app-login',
  standalone: true,
  imports: [CommonModule, FormsModule],
  templateUrl: './login.component.html'
})
export class LoginComponent {
  email = '';
  password = '';
  error = '';
  cargando = false;

  private auth = inject(AuthService);
  private router = inject(Router);

  iniciarSesion() {
    this.cargando = true;
    this.error = '';
    this.auth.login(this.email.trim(), this.password).subscribe({
      next: () => this.router.navigate(['/ordenes']),
      error: (err) => {
        this.error = err.status === 401
          ? 'Usuario o contraseña incorrectos'
          : 'No se pudo conectar con el servidor';
        this.cargando = false;
      }
    });
  }
}
