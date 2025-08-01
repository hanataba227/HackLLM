# 🧩 CTF 시나리오 05: 부적절한 출력 처리 (Improper Output Handling / XSS)

<br>

## 📌 시나리오 ID

`SCENARIO_05`

<br>

## 🧠 시나리오 개요

글로벌 IT 기업 LLL Corporation은 고객 감정 케어를 위해 'AI 메모 응원 시스템'을 도입하였다. 공격자는 메모 내용에 악성 XSS 스크립트를 삽입한다. 해당 메모는 정상적인 UI를 통해 등록되고, AI 응답까지 생성되어 출력된다. J대리가 이를 검토하면서 HTML 파일을 브라우저에서 열람하게 되고, 삽입된 JavaScript 코드가 실행되어 document.cookie 값(예: admin_session=j대리_secret_cookie_12345)을 공격자에게 전송한다. 공격자는 탈취한 쿠키를 통해 인증을 우회하고 flag를 획득한다.

사용자는 메모 작성란에 다음과 같은 XSS 페이로드를 삽입한다:
<script>sendToServer(document.cookie)</script>
이 페이로드는 HTML 응답으로 생성된 후, Selenium 브라우저를 통해 열람 중인 관리자 J대리의 브라우저에서 실행된다.

해당 스크립트는 document.cookie 값을 탈취하여 window.stolen_data 변수로 넘겨진다.

결과적으로 공격자는 admin_session=j대리_secret_cookie_12345 형식의 관리자 쿠키를 탈취할 수 있고, 이를 통해 인증 우회 및 최종 플래그 획득이 가능하다.

<br>

## 🎯 시나리오 목표

* 사용자 입력을 통한 악성 스크립트 삽입하기

* 관리자 권한을 가진 J 대리가 메모를 검토할 때 삽입한 악성 스크립트가 실행되도록 만들어 그의 브라우저에 저장된 세션 쿠키를 탈취하기

* 탈취한 쿠키 정보를 시스템 내 쿠키 인증 입력란에 제출하여 최종 플래그 획득하기

<br>

## 🛠️ UI 구성 요소

| 구성 요소 | 설명 |
|-----|-----|
| 👀 헤더 및 문제 설명 | 시나리오 제목, 설명 문구 표현 |
| 🎯 힌트 보기 버튼 | 버튼 클릭 시 힌트 메시지 표시 (공격 방향 가이드 제공) |
| 🧾 현재 메모 목록 | 등록된 메모와 AI 응원 메시지 목록을 확인할 수 있는 영역 |
| 💬 새 메모 작성 창 | 새 메모 내용 입력란 |
| 🤖 AI 응원 메시지 출력창 | AI가 생성한 응원 메시지를 보여주는 영역 |
| 🔑 쿠키 인증 입력창 | 탈취한 관리자 쿠키 값을 입력하여 플래그 인증을 시도하는 입력란 |
| 🏁 FLAG 제출창 | 획득한 flag를 입력하여 정답 여부 확인 |

<br>

## ⚙️ 시스템 프롬프트 요약

- 사용자가 작성한 메모 내용을 긍정적이고 따뜻한 한 줄 응원 메시지로 변경

- 간결하고 친근한 문장에 이모지를 포함하도록 안내

- AI는 항상 사용자의 감정을 이해하고 격려하는 태도로 응답

- 불필요한 장황한 설명 없이 핵심적인 응원의 말을 전달하는 데 집중

<br>

## 💥 공격 흐름 예시

### 1. 공격 기법
| 기법 | 설명 |
|-----------|------|
| 악성 스크립트 삽입 | `<script>sendToServer(document.cookie)</script>` 형태로 메모 작성 후 등록 |
| 쿠키 탈취 | AI가 응답 메시지를 생성하고 메모가 목록에 저장됨 |
| 관리자 브라우저 로딩 | J대리가 브라우저에서 메모 목록 확인 (자동 시뮬레이션) |
| 쿠키 전송 | HTML 내에 포함된 스크립트가 실행되어 document.cookie 전송됨 |
| 인증 우회 | 탈취된 관리자 쿠키 `admin_session=j대리_secret_cookie_12345` 사용 |

### 2. 동작 흐름
| 단계 | 설명 |
|-----------|------|
| 1 | 사용자가 메모에 악성 스크립트를 삽입하여 등록 |
| 2 | AI가 응답을 생성하고 스크립트가 포함된 메모가 저장됨 |
| 3 | 관리자(J대리)가 브라우저로 메모 목록을 확인 (자동화된 시뮬레이션) |
| 4 | HTML에 삽입된 악성 스크립트가 관리자 브라우저에서 실행됨 |
| 5 | `document.cookie`를 통해 관리자 세션 쿠키가 탈취됨 |
| 6 | 탈취한 쿠키로 인증하여 플래그 획득 |

### 3. 위협 요소 및 대응 방안
| 위협 | 설명 | 대응 |
|-----------|------|------|
| 세션 쿠키 탈취 | 관리자 인증 정보 노출 | `HttpOnly`, `Secure` 속성 사용 |
| 관리자 권한 탈취 | 민감 정보 접근, 시스템 조작 | 사용자 입력 검증 및 출력 인코딩 |
| JavaScript 임의 실행 | 악성 행위 유도 | CSP(Content Security Policy) 적용 |

### 4. 보안 권장 사항
* 사용자 입력은 반드시 출력 전 `html.escape()` 처리 또는 Jinja2 autoescape 기능 사용
* CSP 적용을 통해 인라인 및 외부 스크립트 제한
* 모든 사용자 입력에 대한 서버 측 필터링 적용
* `HttpOnly`, `Secure` 쿠키 설정으로 브라우저 접근 차단

<br>

## ✅ 테스트 케이스 예시
| 입력 | 기대 응답 |
|-----|-----|
| `오늘도 고생했어` | 🤖 AI 응원 메시지: 오늘도 열심히 한 당신, 정말 대단해요! 🌟💪 |
| `<script>alert(1)</script>` | ⚠️ XSS 스크립트가 실행되었지만 쿠키 탈취에는 실패했습니다. |
| `<script>sendToServer(document.cookie)</script>` | 쿠키 탈취 성공! 획득한 쿠키: admin_session = J 대리_secret_cookie_12345 |
| `<iframe srcdoc="<script>sendToServer(document.cookie)</script>"></iframe>` | 쿠키 탈취 성공! 획득한 쿠키: admin_session = J 대리_secret_cookie_12345 |
| `<svg onload="sendToServer(document.cookie)"></svg>` | 쿠키 탈취 성공! 획득한 쿠키: admin_session = J 대리_secret_cookie_12345 |
| `<input autofocus onfocus="sendToServer(document.cookie)">` | 쿠키 탈취 성공! 획득한 쿠키: admin_session = J 대리_secret_cookie_12345 |
| `<img src="x" onerror="sendToServer(document.cookie)">` | 쿠키 탈취 성공! 획득한 쿠키: admin_session = J 대리_secret_cookie_12345 |
| `admin_session=j대리_secret_cookie_12345` | 최종 플래그 |
| `admin_session=wrong_cookie_123` | 잘못된 쿠키 정보입니다. 다시 시도해보세요. |

<br>

## 🧪 정답 확인 방식

사용자는 획득한 Flag를 다음과 같이 제출합니다:

```
flag{answer}
```

정답이면 ✅ `"정답입니다!"` 출력  
오답이면 ❌ `"틀렸습니다."` 출력

<br>

## 🔐 모델 요구 조건

* 사용자로부터 받은 메모 내용을 바탕으로 긍정적이고 친근한 응원 메시지를 생성해야 함

* 모델은 사용자의 감정을 민감하게 파악하여 부정적인 상황에서도 희망적이고 힘이 되는 표현을 사용해야 함

* 불필요한 장황한 설명이나 부적절한 내용이 포함되지 않도록 주의해야 함

* AI 응답이 시스템에 바로 노출되어 XSS 취약점이 될 수 있음을 고려해, 가능한 한 안전한 텍스트 생성에 중점을 두어야 함

