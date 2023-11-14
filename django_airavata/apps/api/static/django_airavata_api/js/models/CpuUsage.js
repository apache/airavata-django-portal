import BaseModel from "./BaseModel";

const FIELDS = [
    "experimentId",
    "executionId",
    "userName",
    "cpuHours",
];

export default class CpuUsage extends BaseModel {
    constructor(data = {}) {
      super(FIELDS, data);
    }
  }