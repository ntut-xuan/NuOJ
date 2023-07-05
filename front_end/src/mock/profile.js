import { rest } from "msw";
import monkey from "./coding_monkey.jpeg";

const user_pony = {
  role: 0,
  handle: "pony",
  img: monkey,
  email: "pomy076152340@gmail.com",
  school: "台北科大",
  bio: "真假拉！原神-啟動!小跑豬來了！",
};

export const ProfileHandler = [
  rest.get("/api/profile/:handle", (req, res, ctx) => {
    if (req.params.handle === user_pony.handle) {
      return res(
        ctx.status(200),
        ctx.json({
          role: user_pony.role,
          email: user_pony.email,
          school: user_pony.school,
          bio: user_pony.bio,
        })
      );
    } else {
      return res(ctx.status(403));
    }
  }),

  rest.get("/api/profile/:handle/avatar", async (req, res, ctx) => {
    let handle = req.params.handle;
    if (handle === user_pony.handle) {
      const imageBuffer = await fetch(user_pony.img).then((res) =>
        res.arrayBuffer()
      );

      return res(
        ctx.set("Content-Length", imageBuffer.byteLength.toString()),
        ctx.set("Content-Type", "image/jpeg"),
        ctx.body(imageBuffer)
      );
    } else {
      return res(ctx.status(403));
    }
  }),

  rest.post("/api/profile/:handle", async (req, res, ctx) => {
    let json = await req.json();
    if ("bio" in json) {
      user_pony.bio = json["bio"];
    }
    if ("school" in json) {
      user_pony.school = json["school"];
    }
    return res(ctx.status(200), ctx.json({ status: "ok" }));
  }),
];
