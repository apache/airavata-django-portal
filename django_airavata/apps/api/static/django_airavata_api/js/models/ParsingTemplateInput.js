
import BaseModel from "./BaseModel";

const FIELDS = [
  "id",
  "targetInputId",
  "applicationOutputName",
  "value",
  "parsingTemplateId"
];

export default class ParsingTemplateInput extends BaseModel {
  constructor(data = {}) {
    super(FIELDS, data);
  }
}
