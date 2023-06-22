import { SocialAuthService, SocialUser } from '@abacritt/angularx-social-login';
import { Component } from '@angular/core';
import { Router } from '@angular/router';
import { UserService } from 'src/app/user.service';

@Component({
  selector: 'app-login',
  templateUrl: './login.component.html',
  styleUrls: ['./login.component.css'],
})
export class LoginComponent {
  user!: SocialUser;
  loggedIn!: boolean;

  constructor(
    private authService: SocialAuthService,
    private userService: UserService,
    private router: Router
  ) {}

  ngOnInit() {
    this.authService.authState.subscribe((user) => {
      this.user = user;
      this.loggedIn = user != null;
      console.log(this.user);
      this.sendTokenToBackend(this.user.idToken)
    });
  }

  sendTokenToBackend(token: string) {
    this.userService.authUser(token).subscribe((response) => {
      if (response != "unauthorized") {
      this.router.navigate(['/snippets']);
      alert(response);
      } else {
        alert(response)
      }
    });
  }
}
