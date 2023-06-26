import { CanActivateFn, Router } from '@angular/router';
import { AuthService } from '../services/auth.service';
import { inject } from '@angular/core';

export const authGuard: CanActivateFn = () => {
  const router = inject(Router);

  if (localStorage.getItem('token')) {
    return true;
  }

  console.log("token absent");
  return router.parseUrl('');
}
