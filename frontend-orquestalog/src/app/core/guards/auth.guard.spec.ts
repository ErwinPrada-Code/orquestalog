import { TestBed } from '@angular/core/testing';
import { provideHttpClient } from '@angular/common/http';
import { Router, UrlTree, provideRouter } from '@angular/router';
import { authGuard } from './auth.guard';

function jwtFalso(exp: number): string {
  const payload = btoa(JSON.stringify({ sub: 'a@a.com', nombre: 'A', rol: 'admin', empresa_id: 1, exp }));
  return `x.${payload}.y`;
}

describe('authGuard', () => {
  beforeEach(() => {
    TestBed.configureTestingModule({ providers: [provideHttpClient(), provideRouter([])] });
    TestBed.inject(Router);
    localStorage.removeItem('token');
  });

  afterEach(() => localStorage.removeItem('token'));

  const ejecutar = () => TestBed.runInInjectionContext(() => authGuard({} as any, {} as any));

  it('redirige a /login cuando no hay token', () => {
    const resultado = ejecutar();
    expect(resultado).toBeInstanceOf(UrlTree);
    expect((resultado as UrlTree).toString()).toBe('/login');
  });

  it('redirige a /login cuando el token está vencido', () => {
    localStorage.setItem('token', jwtFalso(Math.floor(Date.now() / 1000) - 60));
    expect(ejecutar()).toBeInstanceOf(UrlTree);
  });

  it('permite el paso con un token vigente', () => {
    localStorage.setItem('token', jwtFalso(Math.floor(Date.now() / 1000) + 3600));
    expect(ejecutar()).toBe(true);
  });
});
