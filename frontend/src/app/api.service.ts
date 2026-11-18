import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { environment } from '../environments/environment';

export interface Product { id:number; code:string; name:string; category:string; quantity:number; minimum_stock:number; active:boolean; }
export interface Movement { id:number; product_id:number; type:string; quantity:number; note:string; created_at:string; }

@Injectable({ providedIn: 'root' })
export class ApiService {
  private token = '';
  constructor(private http: HttpClient) {}
  private headers() { return new HttpHeaders({ Authorization: `Bearer ${this.token}` }); }
  login(username:string,password:string) {
    return this.http.post<{access_token:string}>(`${environment.apiUrl}/api/auth/login`,{username,password});
  }
  setToken(token:string) { this.token = token; }
  products() { return this.http.get<Product[]>(`${environment.apiUrl}/api/products`,{headers:this.headers()}); }
  createProduct(data:Partial<Product>) { return this.http.post<Product>(`${environment.apiUrl}/api/products`,data,{headers:this.headers()}); }
  movement(data:{product_id:number;type:'ENTRADA'|'SAIDA';quantity:number;note:string}) {
    return this.http.post<Movement>(`${environment.apiUrl}/api/movements`,data,{headers:this.headers()});
  }
  summary() { return this.http.get<{products_count:number;low_stock_count:number}>(`${environment.apiUrl}/api/dashboard/summary`,{headers:this.headers()}); }
}
