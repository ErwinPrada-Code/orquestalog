import { ApplicationRef, Injectable, inject, signal } from '@angular/core';

export interface Toast {
  id: number;
  tipo: 'exito' | 'error';
  mensaje: string;
}

@Injectable({ providedIn: 'root' })
export class ToastService {
  readonly toasts = signal<Toast[]>([]);
  private appRef = inject(ApplicationRef);
  private siguienteId = 0;

  exito(mensaje: string): void {
    this.mostrar('exito', mensaje);
  }

  error(mensaje: string): void {
    this.mostrar('error', mensaje);
  }

  cerrar(id: number): void {
    this.toasts.update((lista) => lista.filter((t) => t.id !== id));
    this.appRef.tick();
  }

  private mostrar(tipo: Toast['tipo'], mensaje: string): void {
    const id = ++this.siguienteId;
    this.toasts.update((lista) => [...lista, { id, tipo, mensaje }]);
    this.appRef.tick(); // los callbacks HTTP de este repo no repintan solos
    setTimeout(() => this.cerrar(id), 4000);
  }
}
