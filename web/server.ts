// server.ts - Deno server for the web application
import { serve } from "https://deno.land/std@0.224.0/http/server.ts";
import { dirname, join } from "https://deno.land/std@0.224.0/path/mod.ts";

// Get the directory of the current file
const currentDir = dirname(import.meta.url);

// Serve static files from the out directory (Next.js build output)
const handler = async (req: Request): Promise<Response> => {
  const url = new URL(req.url);
  const pathname = url.pathname;
  
  // Serve static files
  if (pathname.startsWith("/_next/") || pathname.startsWith("/static/")) {
    const filePath = join(currentDir, "out", pathname);
    try {
      const file = await Deno.open(filePath);
      const stat = await file.stat();
      const headers = new Headers();
      headers.set("Content-Length", stat.size.toString());
      return new Response(file.readable, { headers });
    } catch (error) {
      return new Response("File not found", { status: 404 });
    }
  }
  
  // Serve the main page
  if (pathname === "/" || pathname === "/index.html") {
    try {
      const html = await Deno.readTextFile(join(currentDir, "out", "index.html"));
      return new Response(html, {
        headers: { "Content-Type": "text/html" },
      });
    } catch (error) {
      return new Response("Page not found", { status: 404 });
    }
  }
  
  // Default response
  return new Response("Welcome to the Morty Pet Store API");
};

// Start the server
const port = 8000;
console.log(`Server running on http://localhost:${port}`);
await serve(handler, { port });