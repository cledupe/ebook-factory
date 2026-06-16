FROM node:20-alpine AS base

FROM base AS deps
WORKDIR /app
COPY package.json package-lock.json ./
RUN npm ci --only=production

FROM base AS runner
WORKDIR /app
ENV NODE_ENV=production
COPY --from=deps /app/node_modules node_modules
COPY . .
RUN npm run build \
    --if-present \
    || echo "skip build (frontend not ready)"

EXPOSE 3000

CMD ["sh", "-c", "npx next start -p 3000 || echo 'frontend not built'"]
