export function buildEditPrompt(instructions: string): string {
  const base = `You are editing a photo of a 7-Eleven frozen display case in Japan.
Edit ONLY the masked area. Keep everything outside the mask pixel-identical.

Inside the masked area, place the reference products described below.

Strict rules:
- Preserve the exact packaging design, logos, Japanese text, and color of each reference product. Do NOT redraw, restyle, or translate the packaging.
- Match the existing case's lighting, cool color temperature, subtle glass reflection, and slight cold mist.
- Keep price rails, POP tags, and shelf edges in their original positions.
- Photorealistic, straight-on shelf perspective, sharp focus on products.
- No added text, no extra POP, no extra products beyond what is specified.`;

  const userInstructions = instructions.trim();
  if (!userInstructions) return base;

  return `${base}\n\nPlacement instructions:\n${userInstructions}`;
}
