import { auth } from "./auth";

export default auth((req) => {
  // Allow unauthenticated access to the homepage, login page, and NextAuth API routes
  const publicRoutes = ["/auth/sign-in"];
  if (
    !req.auth &&
    !publicRoutes.includes(req.nextUrl.pathname) &&
    !req.nextUrl.pathname.startsWith("/api/auth")
  ) {
    const newUrl = new URL("/auth/sign-in", req.nextUrl.origin);
    return Response.redirect(newUrl);
  }
});

export const config = {
  matcher: [
    // Skip Next.js internals and all static files, unless found in search params
    '/((?!_next|[^?]*\\.(?:html?|css|js(?!on)|jpe?g|webp|png|gif|svg|ttf|woff2?|ico|csv|docx?|xlsx?|zip|webmanifest)).*)',
    // Always run for API routes
    '/(api|trpc)(.*)',
  ],
};