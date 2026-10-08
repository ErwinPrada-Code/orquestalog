import { ComponentFixture, TestBed } from '@angular/core/testing';
import { FormularioOrden } from './formulario-orden';

describe('FormularioOrden', () => {
  let component: FormularioOrden;
  let fixture: ComponentFixture<FormularioOrden>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [FormularioOrden],
    }).compileComponents();

    fixture = TestBed.createComponent(FormularioOrden);
    component = fixture.componentInstance;
    await fixture.whenStable();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
