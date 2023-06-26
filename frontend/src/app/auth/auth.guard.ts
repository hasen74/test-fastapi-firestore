import { CanActivateFn, Router } from '@angular/router';
import { AuthService } from '../services/auth.service';
import { inject } from '@angular/core';

export const authGuard: CanActivateFn = () => {
  const router = inject(Router);
  const authService = inject(AuthService)

  if (localStorage.getItem('token') && authService.user) {
    console.log('token et user présent')
    return true;
  }

  console.log("token absent");
  return router.parseUrl('/login');
}
