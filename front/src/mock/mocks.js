import { setupWorker } from "msw";
import { AuthHandler } from "./auth";

// This configures a Service Worker with the given request handlers.
let Workers = [...AuthHandler];

export const authWorker = setupWorker(...Workers);
