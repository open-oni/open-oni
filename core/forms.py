import datetime

from django import forms
from django.forms import fields
from django.conf import settings
from django.core.cache import cache
from django.db.models import Min, Max

from core import models
from core.utils.utils import fulltext_range

# min and max year set in utils.py
DAY_CHOICES = [(i, i) for i in range(1,32)]
MONTH_CHOICES = ((1, 'Jan',), (2, 'Feb',), (3, 'Mar',),
                 (4, 'Apr',), (5, 'May',), (6, 'Jun',),
                 (7, 'Jul',), (8, 'Aug',), (9, 'Sep',),
                 (10, 'Oct',), (11, 'Nov',), (12, 'Dec',))

FREQUENCY_CHOICES = (
    ("", "Select"),
    ("Daily", "Daily"),
    ("Three times a week", "Three times a week"),
    ("Semiweekly", "Semiweekly"),
    ("Weekly", "Weekly"),
    ("Biweekly", "Biweekly"),
    ("Three times a month", "Three times a month"),
    ("Semimonthly", "Semimonthly"),
    ("Monthly", "Monthly"),
    ("Other", "Other"),
    ("Unknown", "Unknown"),
)

PROX_CHOICES = (
    ("5", "5 words"),
    ("10", "10 words"),
    ("50", "50 words"),
    ("100", "100 words"),
)

RESULT_ROWS = (
    ("20", "20"),
    ("50", "50")
)

RESULT_SORT = (
    ("revelance", "Relevance"),
    ("title", "Title"),
    ("date", "Date")
)


def _distinct_values(model, field, initial_label=None):
    # generates list of unique values in a table for use with ChoiceField
    values = model.objects.values(field).distinct().order_by(field)
    options = [("", initial_label)] if initial_label else []
    options.extend((v[field], v[field]) for v in values)
    return options

def _distinct_title_languages():
    values = models.Title.objects.filter(has_issues=True).values("languages").distinct().order_by("languages")
    options = [("", "All")]
    for value in values:
        lang_code = value["languages"]
        lang = models.Language.objects.get(code=lang_code).name
        options.append((lang, lang))
    return options

def _titles_states():
    """
    returns a tuple of two elements (list of titles, list of states)

    example return value:
    ([('', 'All newspapers'), (u'sn83030214', u'New-York tribune. (New York [N.Y.])')],
     [('', 'All states'), (u'New York', u'New York')])
    """
    titles_states = cache.get("titles_states")
    if not titles_states:
        titles = []
        states = []
        # create a temp Set _states to hold states before compiling full list
        _states = set()
        for title in models.Title.objects.filter(has_issues=True).select_related():
            short_name = title.name.split(":")[0]  # remove subtitle
            title_name = "%s (%s)" % (short_name,
                                      title.place_of_publication)
            titles.append((title.lccn, title_name))
            for p in title.places.all():
                _states.add(p.state)
        _states = [s for s in _states if s is not None]
        for state in _states:
            states.append((state, state))
        states = sorted(states)
        cache.set("titles_states", (titles, states))
    else:
        titles, states = titles_states
    return (titles, states)


class CityForm(forms.Form):
    city = fields.ChoiceField(choices=[], required=False)
    city.widget.attrs["class"] = "form-select"
    city.widget.attrs["aria-label"] = "City"
    city.widget.attrs["id"] = "global_city_id"

    def __init__(self, *args, **kwargs):
        super(CityForm, self).__init__(*args, **kwargs)
        cities = (models.Place
                  .objects
                  .filter(titles__has_issues=1)
                  .order_by('city')
                  .values('city')
                  .distinct())
        city = [("", "All Cities")]
        city.extend((p["city"], p["city"]) for p in cities)
        self.fields["city"].choices = city


class SearchPagesFormBase(forms.Form):
    state = fields.ChoiceField(choices=[], required=False)
    date1 = fields.ChoiceField(choices=[], required=False)
    date2 = fields.ChoiceField(choices=[], required=False)
    proxtext = fields.CharField(required=False)
    issue_date = fields.BooleanField(required=False)

    def __init__(self, *args, **kwargs):
        super(SearchPagesFormBase, self).__init__(*args, **kwargs)

        self.titles, self.states = _titles_states()

        fulltextStartYear, fulltextEndYear = fulltext_range()

        self.years = [(year, year) for year in range(fulltextStartYear, fulltextEndYear + 1)]
        self.fulltextStartYear = fulltextStartYear
        self.fulltextEndYear = fulltextEndYear

        self.fields["state"].choices = self.states
        self.fields["date1"].choices = self.years
        self.fields["date1"].initial = fulltextStartYear
        self.fields["date2"].choices = self.years
        self.fields["date2"].initial = fulltextEndYear


class SearchResultsForm(forms.Form):
    rows = fields.ChoiceField(label="Rows", choices=RESULT_ROWS)
    sort = fields.ChoiceField(choices=RESULT_SORT)

    # add classes
    rows.widget.attrs["class"] = "form-select"
    sort.widget.attrs["class"] = "form-select"

    def __init__(self, *args, **kwargs):
        super(SearchResultsForm, self).__init__(*args, **kwargs)
        self.fields["rows"].initial = kwargs.get("rows", "20")
        self.fields["sort"].initial = kwargs.get("sort", "relevance")


class SearchPagesForm(SearchPagesFormBase):
    # locations
    city = fields.ChoiceField(label="City", required=False)
    county = fields.ChoiceField(label="County", required=False)
    state = fields.ChoiceField(label="State", required=False)
    # date
    date1 = fields.CharField(required=False)
    date2 = fields.CharField(required=False)
    date_day = fields.ChoiceField(choices=DAY_CHOICES, required=False)
    date_month = fields.ChoiceField(choices=MONTH_CHOICES, required=False)
    # text
    andtext = fields.CharField(label="All of the words", required=False)
    ortext = fields.CharField(label="Any of the words", required=False)
    phrasetext = fields.CharField(label="With the phrase", required=False)
    proxtext = fields.CharField(label="Words", required=False)
    proxdistance = fields.ChoiceField(choices=PROX_CHOICES, label="Distance",
                                      required=False)
    # misc
    lccn = fields.MultipleChoiceField(choices=[], required=False)
    # filters
    frequency = fields.ChoiceField(label="Frequency", required=False)
    language = fields.ChoiceField(label="Language", required=False)

    form_control_items = [
        andtext, ortext, phrasetext, proxtext
    ]

    for item in form_control_items:
        item.widget.attrs["class"] = "form-control"

    form_select_items = [
        city, county, state,
        proxdistance,
        date1, date2, date_day, date_month,
        lccn,
        language, frequency
    ]
    
    for item in form_select_items:
        item.widget.attrs["class"] = "form-select"

    def __init__(self, *args, **kwargs):
        super(SearchPagesForm, self).__init__(*args, **kwargs)

        self.date = self.data.get('date1', '')

        self.fields["lccn"].widget.attrs.update({'size': '8'})
        self.fields["lccn"].choices = self.titles
        self.fields["language"].choices = _distinct_title_languages()

        # locations

        self.fields["city"].choices = _distinct_values(models.Place, "city", "All")
        self.fields["county"].choices = _distinct_values(models.Place, "county", "All")
        self.fields["state"].choices = _distinct_values(models.Place, "state", "All")

        # filters
        self.fields["frequency"].choices = _distinct_values(models.Title, "frequency", "All")


class SearchTitlesForm(forms.Form):
    state = fields.ChoiceField(choices=[], initial="", required=False)
    county = fields.ChoiceField(choices=[], initial="", required=False)
    city = fields.ChoiceField(choices=[], initial="", required=False)
    year1 = fields.ChoiceField(choices=[], label="from", required=False)
    year2 = fields.ChoiceField(choices=[], label="to", required=False)
    terms = fields.CharField(max_length=255, required=False)
    frequency = fields.ChoiceField(choices=FREQUENCY_CHOICES, initial="",
                                   label="Frequency:", required=False)
    language = fields.ChoiceField(choices=[], initial="", label="Language:",
                                  required=False)
    ethnicity = fields.ChoiceField(choices=[], initial="",
                                   label="Ethnicity Press:", required=False)
    labor = fields.ChoiceField(choices=[], initial="", label="Labor Press:",
                               required=False)
    material_type = fields.ChoiceField(choices=[], initial="",
                                       label="Material Type:", required=False)

    form_control_items = [
        state, county, city, terms,
        frequency, language, ethnicity, labor,
        material_type
    ]
    for item in form_control_items:
        item.widget.attrs["class"] = "form-select"

    def __init__(self, *args, **kwargs):
        super(SearchTitlesForm, self).__init__(*args, **kwargs)

        current_year = datetime.date.today().year
        years = list(range(1690, current_year + 1, 10))
        if years[-1] != current_year:
            years.append(current_year)
        choices = [(year, year) for year in years]
        self.fields["year1"].choices = choices
        self.fields["year1"].initial = choices[0][0]
        self.fields["year2"].choices = choices
        self.fields["year2"].initial = choices[-1][0]

        # location
        cities = models.Place.objects.values('city').distinct().order_by("city")
        city = [("", "Select")]
        city.extend((p["city"], p["city"]) for p in cities)
        self.fields["city"].choices = city
        self.fields["city"].label = "City"

        counties = models.Place.objects.values('county').distinct().order_by("county")
        county = [("", "Select")]
        county.extend((p["county"], p["county"]) for p in counties)
        self.fields["county"].choices = county
        self.fields["county"].label = "County"

        states = models.Place.objects.values('state').distinct().order_by("state")
        state = [("", "Select")]
        state.extend((p["state"], p["state"]) for p in states)
        self.fields["state"].choices = state
        self.fields["state"].label = "State"

        language = [("", "Select"), ]
        language.extend((l.name, l.name) for l in models.Language.objects.all())
        self.fields["language"].choices = language

        ethnicity = [("", "Select"), ]
        ethnicity.extend((e.name, e.name) for e in models.Ethnicity.objects.all())
        self.fields["ethnicity"].choices = ethnicity

        labor = [("", "Select"), ]
        labor.extend((l.name, l.name) for l in models.LaborPress.objects.all())
        self.fields["labor"].choices = labor

        material = [("", "Select")]
        material.extend((m.name, m.name) for m in models.MaterialType.objects.all())
        self.fields["material_type"].choices = material
