import { rest } from "msw";

const fake_problems = [
  {
    id: 1231,
    data: {
      content: {
        title: "第一題拉",
        description: "用來模擬的第一題拉",
        input_description: "用來模擬的第一題拉",
        output_description: "用來模擬的第一題拉",
        note: "用來模擬的第一題拉",
      },
      setting: {
        time_limit: "first time limit",
        memory_limit: "first mem limit",
      },
      author: {
        user_uid: "some_uuid",
        handle: "pony",
      },
    },
  },
  {
    id: 1232,
    data: {
      content: {
        title: "第二題拉",
        description: "用來模擬的第二題拉",
        input_description: "用來模擬的第二題拉",
        output_description: "用來模擬\n的第二題拉",
        note: "用來模擬的第二題拉",
      },
      setting: {
        time_limit: "second time limit",
        memory_limit: "second mem limit",
      },
      author: {
        user_uid: "some_uuid2",
        handle: "ponycome",
      },
    },
  },
];

export const ProblemHandler = [
  rest.get("/api/problem", (req, res, ctx) => {
    return res(ctx.status(200), ctx.json(fake_problems));
  }),

  rest.get("/api/problem/:id", (req, res, ctx) => {
    const id = parseInt(req.params.id);
    for (const problem of fake_problems) {
      console.log(problem);
      if (problem.id === id) {
        return res(ctx.status(200), ctx.json(problem));
      }
    }

    return res(ctx.status(403));
  }),
];
