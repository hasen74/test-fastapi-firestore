import { SocialAuthService, SocialUser } from '@abacritt/angularx-social-login';
import { Injectable } from '@angular/core';
import { Router } from '@angular/router';

@Injectable({
  providedIn: 'root',
})
export class AuthService {
  constructor(
    private authService: SocialAuthService,
    private router: Router
  ) {}

  user!: SocialUser;
  isLoggedIn = false;

  redirectUrl: string | null = '/snippets';

  login() {
    this.authService.authState.subscribe((user) => {
      this.user = user;
      this.isLoggedIn = user != null;
      console.log(this.user);
      localStorage.setItem('token', this.user.idToken);
      this.router.navigate(['/snippets']);
    });
  }

  logout(): void {
    this.isLoggedIn = false;
    localStorage.clear();
  }

  getToken() {
    return localStorage.getItem('token');
  }
}
