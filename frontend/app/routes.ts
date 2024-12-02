import { type RouteConfig, index, route, layout } from "@react-router/dev/routes";

export default [
	index("routes/home.tsx"),
	route("blog", "routes/blog.tsx"),
	route("contact", "routes/contact.tsx"),
	route("table", "routes/payments/page.tsx")
	// layout("./auth/layout.tsx", [
  //   route("login", "./auth/login.tsx"),
  //   route("register", "./auth/register.tsx"),
  // ]),

] satisfies RouteConfig;

