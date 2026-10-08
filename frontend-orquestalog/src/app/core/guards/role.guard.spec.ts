import { TestBed } from '@angular/core/testing';
import { provideHttpClient } from '@angular/common/http';
import { Router, UrlTree, provideRouter } from '@angular/router';
import { roleGuard } from './role.guard';

function jwtFalso(rol: string, exp: number): string {
  const payload = btoa(JSON.stringify({ sub: 'a@a.com', nombre: 'A', rol, empresa_id: 1, exp }));
  return `x.${payload}.y`;
}

describe('roleGuard', () => {
  const vigente = () => Math.floor(Date.now() / 1000) + 3600;

  beforeEach(() => {
    TestBed.configureTestingModule({ providers: [provideHttpClient(), provideRouter([])] });
    TestBed.inject(Router);
    localStorage.removeItem('token');
  });

  afterEach(() => localStorage.removeItem('token'));

  const ejecutar = () =>
    TestBed.runInInjectionContext(() => roleGuard('admin', 'gestor')({} as any, {} as any));

  it('redirige a /login cuando no hay sesión', () => {
    const resultado = ejecutar();
    expect(resultado).toBeInstanceOf(UrlTree);
    expect((resultado as UrlTree).toString()).toBe('/login');
  });

  it('redirige a /dashboard cuando el rol no tiene permiso', () => {
    localStorage.setItem('token', jwtFalso('conductor', vigente()));
    const resultado = ejecutar();
    expect(resultado).toBeInstanceOf(UrlTree);
    expect((resultado as UrlTree).toString()).toBe('/dashboard');
  });

  it('permite el paso al gestor', () => {
    localStorage.setItem('token', jwtFalso('gestor', vigente()));
    expect(ejecutar()).toBe(true);
  });

  it('permite el paso al administrador', () => {
    localStorage.setItem('token', jwtFalso('admin', vigente()));
    expect(ejecutar()).toBe(true);
  });
});