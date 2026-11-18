import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { ApiService, Product } from './api.service';

@Component({
  selector: 'app-root', standalone: true, imports: [CommonModule, FormsModule],
  templateUrl: './app.component.html'
})
export class AppComponent implements OnInit {
  page:'login'|'home'|'movement'|'results'|'products' = 'login';
  username='admin'; password=''; error=''; success='';
  products:Product[]=[]; selectedProductId=0; movementType:'ENTRADA'|'SAIDA'='SAIDA';
  quantity=1; note=''; lastMovement:any=null;
  newProduct={code:'',name:'',category:'',quantity:0,minimum_stock:0};
  summary={products_count:0,low_stock_count:0};
  constructor(private api:ApiService) {}
  ngOnInit() {}
  login() {
    this.error='';
    this.api.login(this.username,this.password).subscribe({
      next:r=>{this.api.setToken(r.access_token);this.page='home';this.load();},
      error:()=>this.error='Usuário ou senha inválidos.'
    });
  }
  load() {
    this.api.products().subscribe({next:p=>this.products=p,error:()=>this.error='Não foi possível carregar os produtos.'});
    this.api.summary().subscribe({next:s=>this.summary=s});
  }
  openMovement(){this.error='';this.success='';this.load();this.page='movement';}
  submitMovement() {
    this.error='';this.success='';
    if(!this.selectedProductId || this.quantity<1){this.error='Selecione um produto e informe uma quantidade maior que zero.';return;}
    this.api.movement({product_id:this.selectedProductId,type:this.movementType,quantity:this.quantity,note:this.note}).subscribe({
      next:m=>{this.lastMovement=m;this.success='Movimentação registrada com sucesso.';this.load();this.page='results';},
      error:e=>this.error=e.error?.detail || 'Não foi possível registrar a movimentação.'
    });
  }
  createProduct() {
    this.error='';
    this.api.createProduct(this.newProduct).subscribe({
      next:()=>{this.newProduct={code:'',name:'',category:'',quantity:0,minimum_stock:0};this.load();this.success='Produto cadastrado com sucesso.';},
      error:e=>this.error=e.error?.detail || 'Não foi possível cadastrar o produto.'
    });
  }
  get selectedProduct(){return this.products.find(p=>p.id===this.selectedProductId);}
  lowStock(){return this.products.filter(p=>p.quantity<=p.minimum_stock);}
  logout(){this.page='login';this.password='';this.error='';}
}
