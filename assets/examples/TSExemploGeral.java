package com.dalthed.tucan;

import android.widget.SpinnerAdapter;

import com.dalthed.tucan.Connection.AnswerObject;
import com.dalthed.tucan.Connection.CookieManager;
import com.dalthed.tucan.scraper.EventsScraper;
import com.dalthed.tucan.testmodels.EventsModel;

import org.junit.Test;
import org.junit.runner.RunWith;
import org.robolectric.RobolectricGradleTestRunner;
import org.robolectric.RuntimeEnvironment;
import org.robolectric.annotation.Config;

import java.util.Map;

import static org.junit.Assert.*;

@RunWith(RobolectricGradleTestRunner.class)
@Config(constants = BuildConfig.class)
public class TSExemploGeral extends TestBase {

    public TSExemploGeral() {
        this.resourcesBaseName = "Events";
        this.testClazzModel = EventsModel.class;
    }

    private static final String TAG = "GitAsyncTaskTest";

    private Injector injector;

    public GitAsyncTaskTest() {
        super("com.madgag.agit", DashboardActivity.class);
    }

    private GitTestHelper helper() {
        return AndroidTestEnvironment.helper(getInstrumentation());
    }

    @Override
    public void setUp() throws ClassNotFoundException, InstantiationException, IllegalAccessException {
        Application application = (Application) getInstrumentation().getTargetContext().getApplicationContext();
        injector = RoboGuice.setBaseApplicationInjector(application, RoboGuice.DEFAULT_STAGE,
                newDefaultRoboModule(application),
                override(new AgitModule()).with(new AgitIntegrationTestModule()));
    }

    @Override
    public void tearDown() {
        RoboGuice.util.reset();
    }

    @MediumTest
    public void testCloneRepoWithEmptyBlobInPack() throws Exception {
        Clone cloneOp = new Clone(true, integrationGitServerURIFor("tiny-repo.with-empty-file.git"),
                helper().newFolder());

        Repository repo = executeAndWaitFor(cloneOp);
        assertThat(repo, hasGitObject("e69de29bb2d1d6434b8b29ae775ad8c2e48c5391")); // empty blob
        assertThat(repo, hasGitObject("adcb77d8f74590f54b4c1919b322aed456b22aeb")); // populated blob
    }

    @MediumTest
    public void testCloneNonBareRepoFromLocalTestServer() throws Exception {
        Clone cloneOp = new Clone(false, integrationGitServerURIFor("small-repo.early.git"), helper().newFolder());

        Repository repo = executeAndWaitFor(cloneOp);

        assertThat(repo, hasGitObject("ba1f63e4430bff267d112b1e8afc1d6294db0ccc"));

        File readmeFile = new File(repo.getWorkTree(), "README");
        assertThat(readmeFile, exists());
        assertThat(readmeFile, ofLength(12));
    }

    @MediumTest
    public void testFetchUpdatesOnCloneFromLocalTestServer() throws Exception {
        Clone cloneOp = new Clone(true, integrationGitServerURIFor("small-test-repo.early.git"), helper().newFolder());

        Repository repository = executeAndWaitFor(cloneOp);

        printFetchRefSpecs(repository);

        String initialCommitId = "3974996807a9f596cf25ac3a714995c24bb97e2c", commit1 = "ce1e0703402e989bedf03d5df535401340f54b42";
        assertThat(repository, hasGitObject(initialCommitId));
        assertThat(repository.resolve("master").name(), equalTo(initialCommitId));
        assertThat(repository, not(hasGitObject(commit1)));

        setRemoteUrl(repository, integrationGitServerURIFor("small-test-repo.later.git"));

        executeAndWaitFor(new Fetch(repository, DEFAULT_REMOTE_NAME));

        assertThat(repository, hasGitObject(commit1));
        assertThat(repository.resolve("master").name(), equalTo(commit1));
    }

    private void printFetchRefSpecs(Repository repository) {
        RemoteConfig remoteConfig = remoteConfigFor(repository, DEFAULT_REMOTE_NAME);
        for (RefSpec refSpec : remoteConfig.getFetchRefSpecs()) {
            Log.i(TAG, "refSpec = " + refSpec);
        }
    }

    @MediumTest
    public void testFetchUpdatesFromLocalTestServer() throws Exception {
        Repository repository = helper().unpackRepo("small-test-repo.early.bare.git.zap");
        setRemoteUrl(repository, integrationGitServerURIFor("small-test-repo.later.git"));

        String initialCommitId = "3974996807a9f596cf25ac3a714995c24bb97e2c", commit1 = "ce1e0703402e989bedf03d5df535401340f54b42";
        assertThat(repository, hasGitObject(initialCommitId));
        assertThat(repository.resolve("master").name(), equalTo(initialCommitId));
        assertThat(repository, not(hasGitObject(commit1)));

        executeAndWaitFor(new Fetch(repository, DEFAULT_REMOTE_NAME));

        assertThat(repository, hasGitObject(commit1));
        assertThat(repository.resolve("master").name(), equalTo(commit1));
    }

    @MediumTest
    public void testPullUpdatesFromLocalTestServer() throws Exception {
        Repository repository = helper().unpackRepo("small-test-repo.early.zap");
        setRemoteUrl(repository, integrationGitServerURIFor("small-test-repo.later.git"));
        // Git.wrap(repository).branchCreate().setName("master").setStartPoint("origin/master");

        assertThat(repository, hasGitObject("3974996807a9f596cf25ac3a714995c24bb97e2c"));
        String commit1 = "ce1e0703402e989bedf03d5df535401340f54b42";
        assertThat(repository, not(hasGitObject(commit1)));
        assertFileLength(2, repository.getWorkTree(), "EXAMPLE");

        executeAndWaitFor(new Pull(repository));

        assertThat(repository, hasGitObject(commit1));

        assertFileLength(4, repository.getWorkTree(), "EXAMPLE");
    }

    private void assertFileLength(int length, File workTree, String exampleFile) {
        File readmeFile = new File(workTree, exampleFile);
        assertThat(readmeFile, exists());
        assertThat("len=" + readmeFile.length(), readmeFile, ofLength(length));
    }

    @MediumTest
    public void testCloneRepoUsingRSA() throws Exception {
        Clone cloneOp = new Clone(true, integrationGitServerURIFor("small-repo.early.git").setUser(RSA_USER),
                helper().newFolder());

        assertThat(executeAndWaitFor(cloneOp), hasGitObject("ba1f63e4430bff267d112b1e8afc1d6294db0ccc"));
    }

    @MediumTest
    public void testCloneRepoUsingDSA() throws Exception {
        Clone cloneOp = new Clone(true, integrationGitServerURIFor("small-repo.early.git").setUser(DSA_USER),
                helper().newFolder());

        assertThat(executeAndWaitFor(cloneOp), hasGitObject("ba1f63e4430bff267d112b1e8afc1d6294db0ccc"));
    }

	@Test
	public void saveImage_noImageFile_ko() throws IOException {
	File outputFile = File.createTempFile("prefix", "png", new File("/tmp"));
	ProductImage image = new ProductImage("01010101010101", ProductImageField.FRONT, outputFile);
	Response response = serviceWrite.saveImage(image.getCode(), image.getField(), image.getImguploadFront(), image.getImguploadIngredients(), image.getImguploadNutrition()).execute();
	assertTrue(response.isSuccess());
	assertThatJson(response.body())
		.node("status")
			.isEqualTo("status not ok");
	}

    @MediumTest
    public void testSimpleReadOnlyCloneFromGitHub() throws Exception {
        Clone cloneOp = new Clone(false, new URIish("git://github.com/agittest/small-project.git"),
                helper().newFolder());
        Repository repo = executeAndWaitFor(cloneOp);

        assertThat(repo, hasGitObject("9e0b5e42b3e1c59bc83b55142a8c50dfae36b144"));
        assertThat(repo, not(hasGitObject("111111111111111111111111111111111111cafe")));

        File readmeFile = new File(repo.getWorkTree(), "README");
        assertThat(readmeFile, exists());
    }

    @MediumTest
    public void testNonBareCloneFromRepoWithFiveMBBlobForIssue47() throws Exception {
        Clone cloneOp = new Clone(false, new URIish("git://github.com/rtyley/five-mb-file-test-repo.git"),
                helper().newFolder());
        Repository repo = executeAndWaitFor(cloneOp);

        assertThat(repo, hasGitObject("3995316735a53542acdf0d92e0b725fe296c0b49"));
        assertThat(repo, not(hasGitObject("111111111111111111111111111111111111cafe")));

        File bigFile = new File(repo.getWorkTree(), "5mb.zeros");
        assertThat(bigFile, exists());
    }

    //  @LargeTest
    //  public void testCanCloneAllSuggestedRepos() throws Exception {
    //        for (SuggestedRepo suggestedRepo : SUGGESTIONS) {
    //            Repository repo = executeAndWaitFor(new Clone(true, new URIish(suggestedRepo.getURI()), tempFolder()));
    //            Map<String,Ref> allRefs = repo.getAllRefs();
    //            assertThat(allRefs.size(), greaterThan(0));
    //            assertThat(allRefs.size(), greaterThan(0));
    //        }
    //  }

    private Repository executeAndWaitFor(final GitOperation operation)
            throws InterruptedException, IOException {
        final CountDownLatch latch = new CountDownLatch(1);
        Log.d(TAG, "About to start " + operation);
        new Thread() {
            public void run() {
                Looper.prepare();
                Log.d(TAG, "In run method for " + operation);
                GitAsyncTask task = injector.getInstance(GitAsyncTaskFactory.class).createTaskFor(operation,
                        new OperationLifecycleSupport() {
                            public void startedWith(OpNotification ongoingNotification) {
                                Log.i(TAG, "Started " + operation + " with " + ongoingNotification);
                            }

                            public void publish(Progress progress) {
                            }

                            public void error(OpNotification notification) {
                                Log.i(TAG, "Errored " + operation + " with " + notification);
                            }

                            public void success(OpNotification completionNotification) {
                            }

                            public void completed(OpNotification completionNotification) {
                                Log.i(TAG, "Completed " + operation + " with " + completionNotification);
                                latch.countDown();
                            }
                        });
                task.execute();
                Log.d(TAG, "Called execute() on task for " + operation);
                Looper.loop();
            }
        }.start();
        long startTime = currentTimeMillis();
        Log.i(TAG, "Waiting for " + operation + " to complete - currentThread=" + currentThread());
        // http://stackoverflow.com/questions/5497324/why-arent-java-util-concurrent-timeunit-types-greater-than
        // -seconds-available-in
        boolean timeout = !latch.await(7 * 60, SECONDS);
        long duration = currentTimeMillis() - startTime;
        Log.i(TAG, "Finished waiting - timeout=" + timeout + " duration=" + duration);
        assertThat("Timeout for " + operation, timeout, is(false));
        return FileRepositoryBuilder.create(operation.getGitDir());
    }

    /*@MediumTest
    public void testNonBareCloneFromRepoWithFiveMBBlobForIssue47() throws Exception {
        Clone cloneOp = new Clone(false, new URIish("git://github.com/rtyley/five-mb-file-test-repo.git"),
                helper().newFolder());
        Repository repo = executeAndWaitFor(cloneOp);

        assertThat(repo, hasGitObject("3995316735a53542acdf0d92e0b725fe296c0b49"));
        assertThat(repo, not(hasGitObject("111111111111111111111111111111111111cafe")));

        File bigFile = new File(repo.getWorkTree(), "5mb.zeros");
        assertThat(bigFile, exists());
    }
    */

    private void setRemoteUrl(Repository repository, URIish uri) throws IOException {
        RemoteConfig remoteConfig = remoteConfigFor(repository, DEFAULT_REMOTE_NAME);
        for (URIish urIish : remoteConfig.getURIs()) {
            remoteConfig.removeURI(urIish);
        }
        remoteConfig.addURI(uri);
        remoteConfig.update(repository.getConfig());
        repository.getConfig().save();
    }

    @Test
    public void testSpinner() {

        for (Map.Entry<String, String> entry : sourcesMap.entrySet()) {

            String id = entry.getKey();
            Object resultObject = resultsMap.get(id);
            if (resultObject instanceof EventsModel) {
                EventsModel result = (EventsModel) resultObject;
                if (result.testSpinner.runTest) {
                    System.out.println("Testing " + id + " (testSpinner)");
                    //System.out.println(result);
                    AnswerObject answer = new AnswerObject(entry.getValue(), "", new CookieManager(), "");
                    EventsScraper scraper = new EventsScraper(RuntimeEnvironment.application, answer);
                    SpinnerAdapter spinnerAdapter = scraper.spinnerAdapter();
                    assertEquals(spinnerAdapter.getCount(), result.testSpinner.data.size());
                    for (int i = 0; i < spinnerAdapter.getCount(); i++) {
                        assertEquals(spinnerAdapter.getItem(i), result.testSpinner.data.get(i));
                    }
                }
            }
        }
    }

    @Test
    public void getString_MatchesValuePassedToConstructor() {
        final long value = 1.00;
        final String expectedResult = "1.00";

        Money m = new Money(value);
        String result = m.getLong();
        assertEquals(expectedResult, result);
    }

    @Test
    public void testFlightMileage_asKm2() throws Exception {
        // setup fixture
        // exercise contructor
        Flight newFlight = new Flight(validFlightNumber);
        // verify constructed object
        assertEquals(validFlightNumber, newFlight.number);
        assertEquals("", newFlight.airlineCode);
        assertNull(newFlight.airline);
        // setup mileage
        newFlight.setMileage(1122);
        // exercise mileage translater
        int actualKilometres = newFlight.getMileageAsKm();    
        // verify results
        int expectedKilometres = 1810;
        assertEquals( expectedKilometres, actualKilometres);
        // now try it with a canceled flight:
        newFlight.cancel();
        try {
            newFlight.getMileageAsKm();
            fail("Expected exception");
        } catch (InvalidRequestException e) {
            assertEquals( "Cannot get cancelled flight mileage", e.getMessage());
        }
    }
}
