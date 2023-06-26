import { SocialAuthService, SocialUser } from '@abacritt/angularx-social-login';
import { Injectable } from '@angular/core';
import { Router } from '@angular/router';
import { UserService } from '../user.service';

@Injectable({
  providedIn: 'root',
})
export class AuthService {
  constructor(
    private authService: SocialAuthService,
    private userService: UserService,
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
      this.sendTokenToBackend(this.user.idToken);
    });
  }

  sendTokenToBackend(token: string) {
    this.userService.authUser(token).subscribe((response) => {
      if (response != 'unauthorized') {
        this.router.navigate(['/snippets']);
        alert(response);
      } else {
        alert(response);
      }
    });
  }

  logout(): void {
    this.isLoggedIn = false;
  }
}
