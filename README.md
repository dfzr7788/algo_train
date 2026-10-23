# 算法集训队数据仓库

主页复刻自 https://herkyherky.github.io/ ，保留原有视觉及管理方案，增加每日汇总看板。
当前没有真实训练数据。

## 数据边界
- local/：仅本地保存，Git 忽略。存放成员答案、成员身份、训练计划及原始记录。请自行备份。
- docs/：网站发布目录，只发布团队汇总。不要把个人数据放进这个目录。
- scripts/build.py：白名单导出，不导出成员 ID、题目 ID、答案或计划文本。
- 训练计划、答案可先分别放 local/plans/ 和 local/answers/，当前不自动解析答案、不自动抓取 OJ。
- 参考站的后台接口已断开；不提供在线成员数据编辑功能。

## 每日录入
建立 local/daily.json，初始内容为 []。每个训练场次一个记录，例如：

```json
[{"date":"2026-10-23","participants":["内部成员ID"],"problems":["内部题目ID"],"minutes":120,"accepted":1}]
```

minutes 是该场次所有成员训练分钟之和；accepted 是通过题次（同成员同题只计首次通过，录入前去重）。
一天可有多个场次，参与人数、题目数跨场次去重；分钟与通过题次相加。不要重复录入场次。
示例不是实际数据，勿直接发布。

运行：
```powershell
python scripts/build.py
python -m http.server 8000 --directory docs
```
访问 http://localhost:8000 查看网页。确认汇总后：
```powershell
git add docs scripts README.md .gitignore
git commit -m "Update daily summary"
git push origin main
```

## GitHub Pages
在仓库 Settings → Pages 选择 Deploy from a branch、main、/docs。
私有仓库需要 GitHub Pro 或支持私有 Pages 的套餐；Free 账户应另建仅含公开页面和汇总的公开仓库，不要把本仓库改成公开。
启用成功后预期地址：https://duyan9030-dotcom.github.io/algo_train/ （这不是已上线确认）。
GitHub 同步更新后，Pages 会重新部署。这里未配置每日定时抓取或自动上传本地数据。
