
import BaseModel from "./BaseModel";
import ParserConnectorInput from "./ParserConnectorInput"

const FIELDS = [
  "id",
  "parentParserId",
  "childParserId",
  {
    name: "connectorInputs",
    list: true,
    type: ParserConnectorInput
  },
  "parsingTemplateId"
];

export default class ParserConnector extends BaseModel {
  constructor(data = {}) {
    super(FIELDS, data);
  }
}
