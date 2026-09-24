# TAP Gruntwork Plugin Specification

**Gruntwork infrastructure-as-code as grid vocabulary: v0 carries one outer node, the Gruntwork deployment (the account factory and infrastructure-live estate it manages), so a design can place it before anything is collected.**

## Plugin Identity

| Field | Value |
| --- | --- |
| Slug | `gruntwork` |
| Display name | TAP Gruntwork |
| Description | Gruntwork infrastructure-as-code as grid vocabulary: v0 carries one outer node, the Gruntwork deployment (the account factory and infrastructure-live estate it manages), so a design can place it before anything is collected. |
| Kind | Leaf plugin: Gruntwork vocabulary. Consumes nothing in v0; consumed by instance plugins that place it in a design (highbar first). |

**Default dimensions**

| Dimension | Value | Why |
| --- | --- | --- |
| (none) | | `gruntwork__gruntwork_deployment` declares no default dimension in v0. The only candidate is the `dcom` axis, and its value is a property of the observation, not the type: a seeded design node is `design`, the same type observed by a future collector is `configuration`. The seeding bundle stamps it per node. |

## Philosophy

This is a thin v0 (ruled 2026-09-22 for the highbar starter set): it exists to put the piece on the board so a design can reference it, not to model the domain. The full `create-plugin-spec` interview, prior-art search and requirement buy-in run when this plugin grows past v0; nothing here pre-empts them.

The one type, `gruntwork__gruntwork_deployment`, is the outermost thing a reader of a diagram recognises for Gruntwork. Everything inside it (users, groups, policies, projects, sessions) is later vocabulary, added when something observes or designs it.

Three states hold for every observed field: blank means *not observed*, never *empty*. A design-phase node carries only its name; its identifiers stay blank until a collector reads them.

**Provenance markers:** every node of this type seeded in v0 is *designed* (stamped `dcom: design` by the bundle that seeds it). No field is *observed* until the collector (`req-gruntwork-collector`, Backlog) exists.

## Goals

| # | Name | Description |
| --- | --- | --- |
| 1 | On The Board | Exist as an installable plugin so the highbar stack can boot with it. |
| 2 | Designable | Let a design place the Gruntwork outer node before any access exists. |

## Requirements

| RID | Name | Status | Notes |
| --- | --- | --- | --- |
| req-gruntwork-model | [Gruntwork Deployment Model](#gruntwork-deployment-model) | Implemented | The one outer node: its fields, natural key, icon and display |
| req-gruntwork-record | [CI Record and Tests](#ci-record-and-tests) | Implemented | The in-package `ci` boot record and the manifest/behaviour tests |
| req-gruntwork-collector | [Collector](#collector) | Backlog | Observe real Gruntwork state onto the grid; deferred until access exists |

---

### Gruntwork Deployment Model
----
RID: `req-gruntwork-model`

Status: `Implemented`

A Gruntwork deployment: the Gruntwork-managed estate (account factory, infrastructure-live repository and pipelines) that provisions and governs a set of cloud accounts.

#### Implementation

`tap_plugin/gruntwork/models/gruntwork_deployment.py` defines `GruntworkDeployment(BaseModel)` with `ENTITY_TYPE = "gruntwork__gruntwork_deployment"`, `ENTITY_ICON = "gruntwork-deployment"` (SVG at `static/gruntwork/icons/gruntwork-deployment.svg`), no default dimensions, and fields `name` (required), `repository_url` (The infrastructure-live repository the deployment is driven from. Blank until observed.). It has no free-form `configuration` field and no `tags` map (removed in migration `0003`: nothing read it, and a shapeless map is the same unreviewed-blob risk): no collector exists to fill one, and a verbatim record with no reader is only a place for secret material or personal data to collect, so only promoted columns are stored (migration `0002_drop_unused_configuration` removed it). `NATURAL_KEY = ("name",)`: a design-phase node has no observed identifier, so its name is the only fact it carries; the key is revisited when `req-gruntwork-collector` makes `repository_url` observable.

#### Acceptance Criteria

| ACID | Title | Status | Description | Notes |
| --- | --- | :---: | --- | --- |
| req-gruntwork-model-1 | Created Through The Service Layer | Implemented | A `create_node` write with only `name` succeeds and the row carries it. | |
| req-gruntwork-model-2 | Name Required | Implemented | A `create_node` write without `name` is refused. | |
| req-gruntwork-model-3 | Keyed By Name | Implemented | `NATURAL_KEY` is `("name",)` and every key field is a model field. | |
| req-gruntwork-model-4 | No Free-Form Record | Implemented | The deployment declares no `configuration` field, and a `create_node` write carrying it is refused. | `tests/test_gruntwork_deployment.py` |

---

### CI Record and Tests
----
RID: `req-gruntwork-record`

Status: `Implemented`

The in-package `ci` boot record (`req-boot-bootstrap-ci-record`) and the tests that run in it.

#### Implementation

`tap_plugin/gruntwork/boot/ci.boot.json` installs this plugin alone (it declares no dependencies), offline and credential-free; the consumer flips self to editable. `tap_plugin/gruntwork/tests/test_gruntwork_manifest.py` runs `validate_plugin` at structure and strict levels; `tests/test_gruntwork_deployment.py` covers `req-gruntwork-model`.

#### Acceptance Criteria

| ACID | Title | Status | Description | Notes |
| --- | --- | :---: | --- | --- |
| req-gruntwork-record-1 | Record Declared | Implemented | The manifest declares the `ci` record with its sha256. | |
| req-gruntwork-record-2 | Validates Strict | Implemented | `validate_plugin --strict` passes on the package. | |

---

### Collector
----
RID: `req-gruntwork-collector`

Status: `Backlog`

Observe real Gruntwork state onto the grid; deferred until access exists.

## Model catalog

| Model | Entity type | Category | Rationale |
| --- | --- | --- | --- |
| `GruntworkDeployment` | `gruntwork__gruntwork_deployment` | Outer node | The one node a reader recognises as Gruntwork; everything else nests inside it later. |

## Icons

`gruntwork-deployment` is Gruntwork's own mark, used nominatively to identify the vendor on diagrams. The mark remains its owner's trademark; it is not covered by this repository's licence.
