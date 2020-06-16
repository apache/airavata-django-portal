
import BaseModel from "./BaseModel";

const FIELDS = [
  "id",
  "inputId",
  "parentOutputId",
  "value",
  "parserConnectorId"
];

export default class ParserConnectorInput extends BaseModel {
  constructor(data = {}) {
    super(FIELDS, data);
  }
}
