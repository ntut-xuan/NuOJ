import { setupWorker } from "msw";
import { AuthHandler } from "./auth";
import { ProblemHandler } from "./problem";
import { ProfileHandler } from './profile';

// This configures a Service Worker with the given request handlers.
let Workers = [...AuthHandler, ...ProblemHandler, ...ProfileHandler];

export const workers = setupWorker(...Workers);
