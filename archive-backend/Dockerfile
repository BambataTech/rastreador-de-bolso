FROM node:dubnium-alpine3.9 as build
COPY ./src .
COPY package.json .
COPY tsconfig.json .
COPY tsconfig.build.json .
RUN npm install
RUN npm run build

FROM node:dubnium-alpine3.9
COPY --from=build ./dist /dist
COPY --from=build ./node_modules /node_modules
COPY --from=build ./package.json /package.json
CMD npm run start:prod
