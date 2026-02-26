declare global {
  namespace App {
    interface Error {
      message: string;
    }
    interface Locals {
      apiUrl: string;
    }
    interface PageData {
      apiUrl: string;
    }
  }
}

export {};
