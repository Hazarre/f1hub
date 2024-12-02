import type { Route } from "./+types/home";
import { Welcome } from "../welcome/welcome";

export function meta({}: Route.MetaArgs) {
  return [
    { title: "F1-Hub" },
    { name: "description", content: "Welcome to React Router!" },
  ];
}

export default function Home() {
  return <div>Home</div>;
}
