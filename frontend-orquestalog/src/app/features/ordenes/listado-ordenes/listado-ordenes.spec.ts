import { ComponentFixture, TestBed } from '@angular/core/testing';
import { ListadoOrdenes } from './listado-ordenes';

describe('ListadoOrdenes', () => {
  let component: ListadoOrdenes;
  let fixture: ComponentFixture<ListadoOrdenes>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [ListadoOrdenes],
    }).compileComponents();

    fixture = TestBed.createComponent(ListadoOrdenes);
    component = fixture.componentInstance;
    await fixture.whenStable();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
