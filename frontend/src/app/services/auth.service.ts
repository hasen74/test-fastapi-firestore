import { SocialAuthService, SocialUser } from '@abacritt/angularx-social-login';
import { Injectable, Input } from '@angular/core';
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

  redirectUrl: string | null = '/snippets';

  login() {
    console.log('in login')
    this.authService.authState.subscribe((user) => {
      if (user) {
        console.log('in subscribe')
        this.user = user;
        console.log(this.user);
        localStorage.setItem('token', this.user.idToken);
        localStorage.setItem('name', this.user.name)
        this.router.navigate(['/snippets']);
      }
    });
  }

  logout(): void {
    console.log('in logout')
    localStorage.clear();
  }

  getToken() {
    return localStorage.getItem('token');
  }
}
