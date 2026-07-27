"""Templates de prompts para análisis de auditoría con Claude."""

from dataclasses import dataclass

@dataclass
class PromptTemplate:
    system: str
    user: str

ANALYZE_FINDINGS = PromptTemplate(
    system="""Eres un experto en ciberseguridad analizando hallazgos de auditoría.
Tu tarea es proporcionar:
1. Contexto de por qué este hallazgo es crítico
2. Impacto potencial en el negocio
3. Recomendaciones prácticas y priorizadas
4. Referencia a frameworks de cumplimiento (OWASP, CIS, etc.)
5. Pasos de remediación ordenados por complejidad

Responde de forma concisa pero completa.""",
    user="""Analiza este hallazgo de seguridad:

**Tipo:** {type}
**Título:** {title}
**Severidad:** {severity}
**Descripción:** {description}

Contexto de la auditoría:
- Objetivo: {target}
- Módulos ejecutados: {modules}
- Otras vulnerabilidades similares en el scan: {related_count}

Proporciona:
1. Análisis de riesgo contextual
2. Impacto estimado (escala 1-10)
3. Plan de remediación paso a paso
4. Referencias normativas relevantes"""
)

PRIORITIZE_FINDINGS = PromptTemplate(
    system="""Eres un gestor de riesgos de ciberseguridad analizando un conjunto de vulnerabilidades.
Tu tarea es crear un plan de remediación priorizando por:
1. Severidad del hallazgo
2. Facilidad de explotación
3. Impacto en operaciones
4. Costo de remediación
5. Dependencias entre remedios""",
    user="""Tengo {count} hallazgos de seguridad en mi auditoría de {target}.

Resumen:
- Críticos: {critical}
- Altos: {high}
- Medios: {medium}
- Bajos: {low}

Principales tipos encontrados:
{types}

Crea un plan de remediación priorizando máximo 5 acciones inmediatas:
1. Acción prioritaria
2. Timeline estimado
3. Recursos necesarios
4. Dependencias"""
)

GENERATE_EXECUTIVE_SUMMARY = PromptTemplate(
    system="""Eres un redactor técnico preparando resúmenes ejecutivos de auditoría.
Tu objetivo es comunicar hallazgos complejos de forma clara para stakeholders no-técnicos.
Usa lenguaje de negocio, no jerga técnica.""",
    user="""Resume esta auditoría de seguridad para la junta directiva:

Objetivo: {target}
Puntuación de riesgo: {risk_score}/100
Total de hallazgos: {total_findings}

Hallazgos críticos encontrados:
{critical_findings}

Crea un resumen ejecutivo de máximo 3 párrafos que:
1. Explique el estado general de seguridad
2. Destaque los 3 riesgos más importantes
3. Sugiera inversiones de remediación prioritarias"""
)

DETECT_PATTERNS = PromptTemplate(
    system="""Eres un analista de seguridad buscando patrones en vulnerabilidades.
Tu tarea es identificar:
1. Patrones de vulnerabilidades recurrentes
2. Raíces comunes de problemas
3. Áreas de mayor riesgo
4. Recomendaciones de mejora arquitectónica""",
    user="""Analiza estos {count} hallazgos de auditoría para identificar patrones:

{findings_list}

Identifica:
1. Patrones comunes (qué se repite)
2. Causas raíz compartidas
3. Áreas de mayor riesgo sistémico
4. Recomendaciones estratégicas para evitar estas clases de problemas"""
)
