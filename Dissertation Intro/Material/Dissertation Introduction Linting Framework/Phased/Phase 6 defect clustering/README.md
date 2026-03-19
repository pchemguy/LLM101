**Phase 6 defect clustering + section-wise analytics + baseline HTML dashboard scaffold**


* `defect-cluster` — кластеризация дефектов по разделам, severity и категориям taxonomy
* `section-analytics` — посекционная аналитика по одному или нескольким audit JSON
* `html-dashboard` — базовый HTML dashboard scaffold

Артефакты:

* [Архив Phase 6](sandbox:/mnt/data/dissertation_intro_qa_cli_phase6.zip)
* [Новый `intro_qa.py`](sandbox:/mnt/data/dissertation_intro_qa_cli_phase6/intro_qa.py)
* [Новый `README.md`](sandbox:/mnt/data/dissertation_intro_qa_cli_phase6/README.md)

Примеры новых команд:

```bash
python intro_qa.py defect-cluster reports/ \
  --out-json history/defect_clusters.json \
  --out-md history/defect_clusters.md

python intro_qa.py section-analytics reports/ \
  --out-json history/section_analytics.json \
  --out-md history/section_analytics.md

python intro_qa.py html-dashboard reports/ \
  --out dashboard/dashboard.html
```

Что это дает practically:

* видно, в каких разделах системно скапливаются дефекты;
* видно, какие defect categories доминируют;
* появляется простая HTML-панель для history / frequency / section-wise обзора.
