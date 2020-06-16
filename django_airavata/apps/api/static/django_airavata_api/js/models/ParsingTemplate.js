
import BaseModel from "./BaseModel";
import ParsingTemplateInput from "./ParsingTemplateInput"
import ParserConnector from "./ParserConnector"

const FIELDS = [
  "id",
  "applicationInterface",
  "gatewayId",
  {
    name: "initialInputs",
    list: true,
    type: ParsingTemplateInput
  },
  {
    name: "parserConnections",
    list: true,
    type: ParserConnector
  }
];

export default class ParsingTemplate extends BaseModel {
  constructor(data = {}) {
    super(FIELDS, data);
  }
}
