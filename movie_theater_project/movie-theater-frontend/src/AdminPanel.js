import * as React from "react";
import { Admin, Resource } from "react-admin";
import simpleRestProvider from "ra-data-simple-rest";

import { ListGuesser, EditGuesser } from "react-admin";

const dataProvider = simpleRestProvider("http://localhost:8000/admin");

export default function AdminPanel() {
  return (
    <Admin dataProvider={dataProvider}>
      <Resource name="movies" list={ListGuesser} edit={EditGuesser} />
      <Resource name="showtimes" list={ListGuesser} edit={EditGuesser} />
      <Resource name="auditoriums" list={ListGuesser} edit={EditGuesser} />
    </Admin>
  );
}
